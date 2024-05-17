package system

import (
	"github.com/denisbrodbeck/machineid"
)

// GetHostID gets machine ID or UUID V4
func GetHostID() string {
	id, err := machineid.ProtectedID("paradrop-agent")
	if err != nil {
		return ""
	}
	return id
}
