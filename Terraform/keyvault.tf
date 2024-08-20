provider "azurerm" {
  features {}
}

variable "tenant_id" {
  description = "The Tenant ID for the Azure subscription."
  type        = string
}

variable "object_id" {
  description = "The Object ID of the principal that will be granted access to the Key Vault."
  type        = string
}

variable "resource_group_name" {
  description = "The name of the resource group."
  type        = string
}

variable "location" {
  description = "The location/region where the resource group is created."
  type        = string
}

resource "azurerm_key_vault" "example" {
  name                = "examplekv"
  location            = var.location
  resource_group_name = var.resource_group_name
  sku_name            = "standard"
  tenant_id           = var.tenant_id

  access_policy {
    tenant_id = var.tenant_id
    object_id = var.object_id
    key_permissions = [
      "get",
      "list",
      "create",
      "import",
      "delete",
      "update",
      "sign",
      "verify",
      "wrapKey",
      "unwrapKey",
      "backup",
      "restore"
    ]
    secret_permissions = [
      "get",
      "list",
      "set",
      "delete",
      "recover",
      "backup",
      "restore",
      "purge"
    ]
  }
}

resource "azurerm_key_vault_secret" "example_secret" {
  name         = "example-secret"
  value        = "your-secret-value"
  key_vault_id = azurerm_key_vault.example.id
}