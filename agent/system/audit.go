package system

import (
	"runtime"
	"strings"

	"github.com/MetroStar/paradrop/agent/data"
	"github.com/MetroStar/paradrop/agent/util"
)

// Audit fetches audit rules from auditctl -l Linux command
func Audit(d *data.DiscoverJSON) {
	auditSlice := []string{}

	if runtime.GOOS == "linux" {

		auditctlOut, err := util.Cmd(`auditctl -l`)
		if err != nil {
			d.AuditRules = auditSlice
			return
		}

		auditSlice = append(auditSlice, strings.Split(strings.TrimSpace(string(auditctlOut)), "\n")...)
	}

	d.AuditRules = auditSlice
}
