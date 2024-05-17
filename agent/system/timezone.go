package system

import (
	"runtime"
	"strings"

	"github.com/MetroStar/paradrop/agent/data"
	"github.com/MetroStar/paradrop/agent/util"
)

// TimeZone runs Linux command date to fetch timezone
func TimeZone(d *data.DiscoverJSON) {
	if runtime.GOOS == "windows" {
		return
	}

	dateOut, _ := util.Cmd(`date '+%Z'`)

	timezoneTrim := strings.TrimSpace(string(dateOut))

	d.Timezone = timezoneTrim
}
