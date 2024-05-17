package security

import (
	"runtime"
	"strings"

	"github.com/MetroStar/paradrop/agent/data"
	"github.com/MetroStar/paradrop/agent/util"
)

// CPUvulns detects if CPUs are vulnerable
func CPUVulnerabilities(d *data.DiscoverJSON) {
	cpuVulnerabilities := []string{}

	if runtime.GOOS == "linux" {
		cpuVulns, err := util.Cmd(`grep -r Vulnerable /sys/devices/system/cpu/vulnerabilities`)
		if err != nil {
			d.CPUVulnerabilities = cpuVulnerabilities
			return
		}

		cpuVulnerabilities = append(cpuVulnerabilities, strings.Split(strings.TrimSpace(string(cpuVulns)), "\n")...)
	}

	d.CPUVulnerabilities = cpuVulnerabilities
}
