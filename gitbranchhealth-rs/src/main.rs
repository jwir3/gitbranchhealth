extern crate clap;
use clap::{App, Arg, SubCommand};

fn main() {
    const VERSION: &'static str = env!("CARGO_PKG_VERSION");
    const NAME: &'static str = env!("CARGO_PKG_NAME");
    const AUTHORS: &'static str = env!("CARGO_PKG_AUTHORS");
    const DESCRIPTION: &'static str = env!("CARGO_PKG_DESCRIPTION");

    let matches = App::new(NAME)
        .version(VERSION)
        .author(AUTHORS)
        .about(DESCRIPTION)
        .arg(
            Arg::with_name("log_level")
              .short("v")
              .multiple(true)
              .help("Specify how verbose the output should be")
        )
        .arg(
            Arg::with_name("bad_only")
              .short("b")
              .long("bad-only")
              .help("Only show branches that are ready for pruning (i.e. older than num_days * 2)")
        )
        .arg(
            Arg::with_name("num_days")
              .short("d")
              .takes_value(true)
              .help("Specify number of days old where a branch is considered to no longer be 'healthy'")
              .default_value("14")
        )
        .arg(
            Arg::with_name("no_color")
              .long("no-color")
              .short("n")
              .help("Don't use ANSI colors to display branch health")
        )
        .arg(
            Arg::with_name("repository_path")
              .long("repository_path")
              .short("R")
              .help("Path to git repository where branches should be listed. May be absolute or relative.")
              .default_value(".")
              .takes_value(true)
        )
        .arg(
            Arg::with_name("delete_old")
              .long("delete")
              .short("D")
              .help("Delete old branches that are considered 'unhealthy'")
        )
        .arg(
            Arg::with_name("ignored_branches")
              .short("i")
              .long("ignore-branches")
              .takes_value(true)
              .help("Ignore a set of branches specified by a comma-separated list of branch names")
              .default_value("master")
        )
        .arg(
            Arg::with_name("trunk_branch")
              .short("t")
              .long("trunk")
              .help("Specify the trunk branch name for the given repository")
              .default_value("master")
              .takes_value(true)
        )
        .get_matches();
}
