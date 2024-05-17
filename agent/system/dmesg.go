package system

import (
	"runtime"
	"strings"

	"github.com/MetroStar/paradrop/agent/data"
	"github.com/MetroStar/paradrop/agent/util"
)

// DmesgErrors detects err, emerg, crit, alert messages
func DmesgErrors(d *data.DiscoverJSON) {
	dmesgSlice := []string{}

	if runtime.GOOS == "linux" {

		dmesgOut, _ := util.Cmd(`dmesg -HP --level=err,emerg,crit,alert`)

		dmesgSlice = append(dmesgSlice, strings.Split(strings.TrimSpace(string(dmesgOut)), "\n")...)
	}

	d.DmesgErrors = dmesgSlice
}