#![allow(non_snake_case)]
#[macro_use] 
extern crate rocket;

use rocket::{ 
  http::{Status, ContentType}, 
  serde::{Deserialize, Serialize},
  Responder, response
};


#[derive(Responder)]
#[response(status = 200, content_type = "json")]
struct UserResponse {
  id: u32,
  name: &'static str,
  password: &'static str,
  email: &'static str,
}


#[get("/api/hello")]
fn hello() -> UserResponse {
  let username = "alex1234";
  let password = "Pa$$w0rd";
  let email = "alex@test.com";
  
  UserResponse { 
    id: 1, 
    name: &username, 
    password: &password, 
    email: "alex@test.com" 
  }
}



#[launch]
fn rocket() -> _ {
  rocket::build().mount("/", routes![hello])
}
