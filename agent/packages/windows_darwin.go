//go:build darwin

package packages

import "github.com/MetroStar/paradrop/agent/data"

func WindowsPackages(d *data.DiscoverJSON) {
	wp := []data.WindowsPackages{}
	d.WindowsPackages = wp
}
