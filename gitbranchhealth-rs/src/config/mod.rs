use clap::ArgMatches;

use flexi_logger::{Logger, LogSpecification};

use log::Level;

pub struct BranchHealthConfig {
    repo_path: String,
    remote_name: String,
    num_days: u32,
    bad_only: bool,
    no_color: bool,
    trunk_branch: String,
    // repo: Repository,
    delete_old_branches: bool,
}

impl BranchHealthConfig {
    pub fn new(args: ArgMatches) -> BranchHealthConfig {
        let log_level: Level = match args.occurrences_of("log_level") {
            0 => Level::Error,
            1 => Level::Warn,
            2 => Level::Info,
            3 => Level::Debug,
            4 | _ => Level::Trace
        };

        let num_days: u32 = args.value_of("num_days").unwrap().to_string().parse::<u32>().unwrap();
        let bad_only: bool = match args.value_of("bad_only") {
            Some(_x) => true,
            None => false
        };

        let no_color: bool = match args.value_of("no_color") {
            Some(_x) => true,
            None => false
        };

        let delete_old_branches: bool = match args.value_of("delete_old") {
            Some(_x) => true,
            None => false
        };

        BranchHealthConfig::init_with_options(
            args.value_of("repository_path").unwrap().to_string(),
            args.value_of("remote").unwrap_or("").to_string(), num_days, bad_only, no_color,
            args.value_of("trunk_branch").unwrap().to_string(), delete_old_branches, log_level)
    }

    pub fn init_with_options(repo_path: String, remote_name: String, num_days: u32, bad_only: bool,
                             no_color: bool, trunk_branch: String, delete_old_branches: bool,
                             log_level: Level) -> BranchHealthConfig {
        let mut config = BranchHealthConfig {
            repo_path: repo_path,
            remote_name: remote_name,
            num_days: num_days,
            bad_only: bad_only,
            no_color: no_color,
            trunk_branch: trunk_branch,
            delete_old_branches: delete_old_branches
        };


        config.setup_logging(log_level);

        config
    }

    fn setup_logging(&mut self, log_level: Level) {
        let log_level_str = match log_level {
            Level::Error => "error",
            Level::Warn => "warn",
            Level::Info => "info",
            Level::Debug => "debug",
            Level::Trace => "trace",
        };

        let logger: Logger = Logger::with(LogSpecification::parse(log_level_str).unwrap())
          .format(flexi_logger::colored_detailed_format);
        logger.start().unwrap();
    }
}
