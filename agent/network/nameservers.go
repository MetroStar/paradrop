package network

import (
	"runtime"
	"strings"

	"github.com/MetroStar/paradrop/agent/data"
	"github.com/MetroStar/paradrop/agent/util"
)

// DNS fetches all the DNS servers in resolv.conf
func DNS(d *data.DiscoverJSON) {
	dnsSlice := []string{}

	if runtime.GOOS == "windows" {
		d.DNSNameserver = dnsSlice
		return
	}

	dnsOut, _ := util.Cmd(`grep nameserver /etc/resolv.conf | awk '{ print $2 }'`)

	dnsSlice = append(dnsSlice, strings.Split(strings.TrimSpace(string(dnsOut)), "\n")...)

	d.DNSNameserver = dnsSlice
}