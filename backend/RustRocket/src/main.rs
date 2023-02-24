#[macro_use] 
extern crate rocket;

use rocket::{get, http::Status, serde::json::Json};
use serde::Serialize;


#[derive(Serialize)]
pub struct User {
  pub name: String,
  pub password: String,
  pub email: String,
}

#[get("/hello")]
pub async fn hello() -> Result<Json<User>, Status> {
  let user = User {
    name: "bob1234".to_string(),
    password: "Pa$$w0rd".to_string(),
    email: "bob@test.com".to_string()
  };
  Ok(Json(user))
}



#[launch]
fn rocket() -> _ {
  rocket::build().mount("/", routes![hello])
}
