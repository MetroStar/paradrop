package config

import (
	"github.com/MetroStar/paradrop/agent/data"
)

// Tags parses tags in config file
func Tags(d *data.DiscoverJSON) {
	d.Tags = GetStringSlice("tags")
}
