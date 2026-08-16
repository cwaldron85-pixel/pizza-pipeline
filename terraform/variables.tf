variable "instance_type" {
  description = "EC2 instance size"
  type        = string
  default     = "t2.micro"
}

variable "my_ip" {
  description = "Public IP address allowed to SSH into the instance"
  type        = string
  default     = "0.0.0.0"
}

variable "key_name" {
  description = "Name of the AWS key pair to use"
  type        = string
  default     = "vockey"
}
