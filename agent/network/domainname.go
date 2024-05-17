package network

import (
	"os"
	"strings"

	"github.com/MetroStar/paradrop/agent/data"
)

// DomainName fetches the domain name used on system
func DomainName(d *data.DiscoverJSON) {
	hostname, err := os.Hostname()
	if err != nil {
		return
	}

	if strings.ContainsAny(hostname, ".") {
		d.Domain = strings.TrimSuffix(hostname, ".")
	}
}