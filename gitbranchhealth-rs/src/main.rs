#[macro_use] extern crate log;

extern crate gitbranchhealth;
use gitbranchhealth::app::BranchHealthApplication;

fn main() {
    let app = BranchHealthApplication::new();

    warn!("Application created!");
}
