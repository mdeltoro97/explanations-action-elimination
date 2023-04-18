import errno
import json
import logging
import os.path
import shutil
import signal
import subprocess
import sys
import re
import time

from . import call
from . import limits
from . import portfolio_runner
from . import returncodes
from . import util
from .plan_manager import PlanManager

# TODO: We might want to turn translate into a module and call it with "python3 -m translate".
REL_TRANSLATE_PATH = os.path.join("translate", "translate.py")
REL_ACTION_ELIMINATION_PATH = os.path.join("translate", "action_elim.py")
if os.name == "posix":
    REL_SEARCH_PATH = "downward"
    VALIDATE = "validate"
elif os.name == "nt":
    REL_SEARCH_PATH = "downward.exe"
    VALIDATE = "validate.exe"
else:
    returncodes.exit_with_driver_unsupported_error("Unsupported OS: " + os.name)

def get_executable(build, rel_path):
    # First, consider 'build' to be a path directly to the binaries.
    # The path can be absolute or relative to the current working
    # directory.
    build_dir = build
    if not os.path.exists(build_dir):
        # If build is not a full path to the binaries, it might be the
        # name of a build in our standard directory structure.
        # in this case, the binaries are in
        #   '<repo-root>/builds/<buildname>/bin'.
        build_dir = os.path.join(util.BUILDS_DIR, build, "bin")
        if not os.path.exists(build_dir):
            returncodes.exit_with_driver_input_error(
                "Could not find build '{build}' at {build_dir}. "
                "Please run './build.py {build}'.".format(**locals()))

    abs_path = os.path.join(build_dir, rel_path)
    if not os.path.exists(abs_path):
        returncodes.exit_with_driver_input_error(
            "Could not find '{rel_path}' in build '{build}'. "
            "Please run './build.py {build}'.".format(**locals()))

    return abs_path


def run_translate(args):
    logging.info("Running translator.")
    time_limit = limits.get_time_limit(
        args.translate_time_limit, args.overall_time_limit)
    memory_limit = limits.get_memory_limit(
        args.translate_memory_limit, args.overall_memory_limit)
    translate = get_executable(args.build, REL_TRANSLATE_PATH)
    assert sys.executable, "Path to interpreter could not be found"
    cmd = [sys.executable] + [translate] + args.translate_inputs + args.translate_options

    stderr, returncode = call.get_error_output_and_returncode(
        "translator",
        cmd,
        time_limit=time_limit,
        memory_limit=memory_limit)

    # We collect stderr of the translator and print it here, unless
    # the translator ran out of memory and all output in stderr is
    # related to MemoryError.
    do_print_on_stderr = True
    if returncode == returncodes.TRANSLATE_OUT_OF_MEMORY:
        output_related_to_memory_error = True
        if not stderr:
            output_related_to_memory_error = False
        for line in stderr.splitlines():
            if "MemoryError" not in line:
                output_related_to_memory_error = False
                break
        if output_related_to_memory_error:
            do_print_on_stderr = False

    if do_print_on_stderr and stderr:
        returncodes.print_stderr(stderr)

    if returncode == 0:
        return (0, True)
    elif returncode == 1:
        # Unlikely case that the translator crashed without raising an
        # exception.
        return (returncodes.TRANSLATE_CRITICAL_ERROR, False)
    else:
        # Pass on any other exit code, including in particular signals or
        # exit codes such as running out of memory or time.
        return (returncode, False)


def transform_task(args):
    logging.info("Run task transformation (%s)." % args.transform_task)
    time_limit = limits.get_time_limit(None, args.overall_time_limit)
    memory_limit = limits.get_memory_limit(None, args.overall_memory_limit)
    options = []
    if args.transform_task_options:
        options = args.transform_task_options.split(",")
        for i, option in enumerate(options):
            if i % 2 == 0:
                options[i] = "--" + option

    if not shutil.which(args.transform_task):
        preprocessor_name = "preprocess-h2"
        if args.transform_task != preprocessor_name:
            sys.exit(f"Error: {args.transform_task} not found. Is it on the PATH?")
        # Check if executable exists in the "bin" directory.
        args.transform_task = get_executable(args.build, preprocessor_name)

    try:
        call.check_call(
            "transform-task",
            [args.transform_task] + options,
            stdin=args.sas_file,
            time_limit=time_limit,
            memory_limit=memory_limit)
    except subprocess.CalledProcessError as err:
        if err.returncode != -signal.SIGXCPU:
            returncodes.print_stderr(
                f"Task transformation returned exit status {err.returncode}")


def run_search(args):
    logging.info("Running search (%s)." % args.build)
    time_limit = limits.get_time_limit(
        args.search_time_limit, args.overall_time_limit)
    memory_limit = limits.get_memory_limit(
        args.search_memory_limit, args.overall_memory_limit)
    executable = get_executable(args.build, REL_SEARCH_PATH)

    plan_manager = PlanManager(
        args.plan_file,
        portfolio_bound=args.portfolio_bound,
        single_plan=args.portfolio_single_plan)
    plan_manager.delete_existing_plans()

    if args.portfolio:
        assert not args.search_options
        logging.info("search portfolio: %s" % args.portfolio)
        return portfolio_runner.run(
            args.portfolio, executable, args.search_input, plan_manager,
            time_limit, memory_limit, args)
    else:
        if not args.search_options:
            returncodes.exit_with_driver_input_error(
                "search needs --alias, --portfolio, or search options")
        if "--help" not in args.search_options:
            args.search_options.extend(["--internal-plan-file", args.plan_file])
        try:
            call.check_call(
                "search",
                [executable] + args.search_options,
                stdin=args.search_input,
                time_limit=time_limit,
                memory_limit=memory_limit)
        except subprocess.CalledProcessError as err:
            # TODO: if we ever add support for SEARCH_PLAN_FOUND_AND_* directly
            # in the planner, this assertion no longer holds. Furthermore, we
            # would need to return (err.returncode, True) if the returncode is
            # in [0..10].
            # Negative exit codes are allowed for passing out signals.
            assert err.returncode >= 10 or err.returncode < 0, "got returncode < 10: {}".format(err.returncode)
            return (err.returncode, False)
        else:
            return (0, True)


def run_validate(args):
    logging.info("Running validate.")

    num_files = len(args.filenames)
    if num_files == 1:
        task, = args.filenames
        domain = util.find_domain_filename(task)
    elif num_files == 2:
        domain, task = args.filenames
    else:
        returncodes.exit_with_driver_input_error("validate needs one or two PDDL input files.")

    plan_files = list(PlanManager(args.plan_file).get_existing_plans())
    if not plan_files:
        print("Not running validate since no plans found.")
        return (0, True)
    validate_inputs = [domain, task] + plan_files

    try:
        call.check_call(
            "validate",
            [VALIDATE] + validate_inputs,
            time_limit=args.validate_time_limit,
            memory_limit=args.validate_memory_limit)
    except OSError as err:
        if err.errno == errno.ENOENT:
            returncodes.exit_with_driver_input_error("Error: {} not found. Is it on the PATH?".format(VALIDATE))
        else:
            returncodes.exit_with_driver_critical_error(err)
    else:
        return (0, True)

def run_eliminate_actions(args):
    def parse_plan_filter_skip_actions(planfile):
        MACRO_OP_STRING = "-triv-nec-macro-"
        SKIP_OP_STRING = "(skip-action plan-pos-"
        with open(planfile) as stream:
            lines = stream.readlines()
        plan = []
        for op in lines[:-1]:
            if op.startswith("(" + MACRO_OP_STRING):
                # Kind of messy, might refactor
                plan += list(map(lambda x: f"({x.lstrip('(')}".strip("\n").rstrip(')') + ')', op.split(MACRO_OP_STRING)))[1:]
            elif not op.startswith(SKIP_OP_STRING):
                plan.append(op.strip())
        total_cost = int(re.match(r"; cost = (\d+) \(.+ cost\)", lines[-1]).group(1))
        return plan, total_cost

    def parse_original_action_costs():
        ORGINAL_OP_COSTS_FILE = 'original-op-costs.txt'
        with open(ORGINAL_OP_COSTS_FILE, 'r') as op_cost_file:
            cost_scaling_info = json.loads(op_cost_file.read())
        return cost_scaling_info["num_zero_cost_operators"], cost_scaling_info["original_costs"]

    logging.info("Eliminate actions")

    plan_manager = PlanManager(
        args.plan_file,
        portfolio_bound=args.portfolio_bound,
        single_plan=False)

    # Get last found plan using plan_manager
    plan_files = list(PlanManager(args.plan_file).get_existing_plans())
    if not plan_files:
        print("Not running action elimination since no plans found.")
        return (0, True)

    # Add found plan to manager...
    plan_manager.process_new_plans()
    old_plan_cost = plan_manager.get_next_portfolio_cost_bound()

    # Store plan file in not definitive file before filtering actions
    unfiltered_plan_file = "plan_with_skip_actions"
    ae_plan_file = plan_manager._get_plan_file(len(plan_files) + 1)

    time_limit = limits.get_time_limit(None, args.overall_time_limit)
    memory_limit = limits.get_memory_limit(None, args.overall_memory_limit)

    ae_options = args.action_elimination_options
    planner_options = ["--internal-plan-file", unfiltered_plan_file] + args.action_elimination_planner_configuration

    # Action elimination produced task file is always this one
    ae_task_file = "action-elimination.sas"

    assert sys.executable, "Path to interpreter could not be found"
    action_elimination = get_executable(args.build, REL_ACTION_ELIMINATION_PATH)
    last_plan_file = plan_manager._get_plan_file(plan_manager.get_plan_counter())
    cmd = [sys.executable, action_elimination] + ae_options + ["-t", args.sas_file, "-p", last_plan_file]
    logging.info("Creating action elimination task.")
    try:
        call.check_call(
            "action-elimination",
            cmd,
            time_limit=time_limit,
            memory_limit=memory_limit)
    except subprocess.CalledProcessError as err:
        returncodes.print_stderr(
                f"Error while eliminating actions. Exit status {err.returncode}")
        return err.returncode, False

    executable = get_executable(args.build, REL_SEARCH_PATH)
    logging.info("Running search for action elimination task.")

    try:
        ae_planner_call_time = time.time()
        call.check_call(
                "search",
                [executable] + planner_options,
                stdin=ae_task_file,
                time_limit=time_limit,
                memory_limit=memory_limit)
        ae_planner_call_time = time.time() - ae_planner_call_time
        logging.info(f"AE planner call time: {ae_planner_call_time:3f}")
    except subprocess.CalledProcessError as err:
            assert err.returncode >= 10 or err.returncode < 0, "got returncode < 10: {}".format(err.returncode)
            returncodes.print_stderr(
                f"Error while running search for eliminating actions. Exit status {err.returncode}")
            return (err.returncode, False)

    # Remove skip actions if present in plan
    cleaned_plan, plan_cost = parse_plan_filter_skip_actions(unfiltered_plan_file)

    # If cost scaling was done, we need to map back action costs
    if 'MR' in ae_options and '--no-cost-scaling' not in ae_options:
        num_zero_cost_ops, original_op_costs_map = parse_original_action_costs()
        if num_zero_cost_ops != 0:
            plan_cost = sum([original_op_costs_map[op] for op in cleaned_plan])

    os.remove(unfiltered_plan_file)
    cleaned_plan.append("; cost = %d (%s)" % (plan_cost, "general cost" \
                        if plan_manager.get_problem_type() == "general cost" else "unit cost"))

    logging.info("Old plan cost: %d" % old_plan_cost)
    logging.info("New plan cost: %d" % plan_cost)

    # Write cleaned plan to file
    if old_plan_cost > plan_cost:
        with open(ae_plan_file, 'w') as found_plan:
            found_plan.write("\n".join(cleaned_plan))
            found_plan.write("\n")

    return 0, True
