module "eks_cluster" {
  source = "github.com/terraform-aws-modules/terraform-aws-eks"

  cluster_name        = "revwallet-eks-cluster"
  cluster_version     = "1.21"
  vpc_id              = module.vpc.vpc_id
  subnet_ids          = module.vpc.private_subnet_ids

  tags = {
    Terraform   = "true"
  }
}