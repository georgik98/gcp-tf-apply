output "vpc_network_name" {
  value = module.vpc.vpc_network_name
}

output "subnetwork_name" {
  value = module.vpc.subnetwork_name
}

output "app_engine_url" {
  value = module.app_engine.app_engine_url
}
