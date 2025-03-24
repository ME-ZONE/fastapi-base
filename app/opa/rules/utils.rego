package utils

import rego.v1

## Variable ##
CREATE := "create"

READ := "read"

LIST := "list"

UPDATE := "update"

DELETE := "delete"

## Function ##
is_resource_owner if {
	input.auth.user.id == input.resource.owner.id
}
