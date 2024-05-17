package packages

import (
	"runtime"
	"strings"

	"github.com/MetroStar/paradrop/agent/data"
	"github.com/MetroStar/paradrop/agent/util"
)

// Snaps fetches all snap containers
func Snaps(d *data.DiscoverJSON) {
	snapSlice := []string{}

	if runtime.GOOS == "linux" {

		snapOut, err := util.Cmd(`snap list | awk '/^[a-z]/{print$1"-"$2}'`)
		if err != nil {
			return
		}

		snapSlice = append(snapSlice, strings.Split(strings.TrimSpace(string(snapOut)), "\n")...)
	}

	d.Snaps = snapSlice
}
