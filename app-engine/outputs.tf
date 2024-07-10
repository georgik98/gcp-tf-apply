output "app_engine_url" {
  value = "https://${google_app_engine_application.app.id}.appspot.com"
}