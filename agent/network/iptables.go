package network

import (
	"runtime"
	"strings"

	"github.com/MetroStar/paradrop/agent/data"
	"github.com/MetroStar/paradrop/agent/util"
)

// IPTables fetches all iptables rules
func IPTables(d *data.DiscoverJSON) {
	iptablesSlice := []string{}

	if runtime.GOOS == "linux" {

		iptablesOut, err := util.Cmd(`iptables -L | grep -v '^Chain\|taget\|^$'`)
		if err != nil {
			d.Iptables = iptablesSlice
			return
		}

		for _, line := range strings.Split(strings.TrimSuffix(string(iptablesOut), "\n"), "\n") {
			iptablesSlice = append(iptablesSlice, strings.TrimSpace(line))
		}
	}

	d.Iptables = iptablesSlice
}
