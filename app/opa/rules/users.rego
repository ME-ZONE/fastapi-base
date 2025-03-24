package users

import data.utils
import rego.v1

## Variable ##
default allow := false

default filter := []

## Allow condition ##

allow if {
	input.scope == utils.CREATE
	input.auth.user.is_superuser
}

## Reasons condition ##
reasons[msg] if {
	input.scope == utils.CREATE
	not input.auth.user.is_superuser
	msg := "Tài nguyên thuộc về quản trị viên."
}

## Result ##
result := {
	"allow": allow,
	"reasons": reasons,
}

## Filter RPN ##
filter := qobject if {
	input.auth.user.is_superuser
	qobject = []
}

filter := qobject if {
	not input.auth.user.is_superuser
	qobject = [{"id": input.auth.user.id}]
}

## Function ##
