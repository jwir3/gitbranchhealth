extern crate gitbranchhealth;
use gitbranchhealth::BranchHealthConfig;

#[macro_use] extern crate log;
use log::Level;

#[test]
fn it_should_log_correctly() {
    let config: BranchHealthConfig
      = BranchHealthConfig::init_with_options(".".to_string(), "origin".to_string(), 14, false,
                                              false, "master".to_string(), false, Level::Warn);
    info!("This should not be logged");
    warn!("This should be logged");
}
