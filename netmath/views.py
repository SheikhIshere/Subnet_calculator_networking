from django.shortcuts import render
from .models import SubnetCalculation
import ipaddress

def prefix_to_binary_mask(prefix_len):
    bits = '1' * prefix_len + '0' * (32 - prefix_len)
    return '.'.join(bits[i:i+8] for i in range(0, 32, 8))

def subnet_calculator(request):
    context = {}

    if request.method == 'POST':
        cidr_input = request.POST.get('cidr_input')

        try:
            network = ipaddress.ip_network(cidr_input, strict=False)

            subnet_mask = str(network.netmask)
            total_ip = network.num_addresses
            if network.prefixlen >= 31:
                usable_host = total_ip
            else:
                usable_host = total_ip - 2

            network_address = str(network.network_address)
            broadcast_address = str(network.broadcast_address)

            if usable_host == 0:
                first_host = last_host = None
            elif usable_host == total_ip:
                first_host = str(network.network_address)
                last_host = str(network.broadcast_address)
            else:
                first_host = str(list(network.hosts())[0])
                last_host = str(list(network.hosts())[-1])

            binary_mask = prefix_to_binary_mask(network.prefixlen)

            # Save to DB
            result = SubnetCalculation.objects.create(
                cidr_input=cidr_input,
                binary_num=binary_mask,
                subnet_mask=subnet_mask,
                total_ip=total_ip,
                usable_host=usable_host,
                network_address=network_address,
                first_host=first_host,
                last_host = last_host,
                broadcast_address=broadcast_address,
            )

            context['result'] = result
            context.update({
                'network_address': network_address,
                'broadcast_address': broadcast_address,
                'first_host': first_host,
                'last_host': last_host,
            })

        except ValueError:
            context['error'] = "Invalid CIDR - হালার-পু ভ্যালিডটা দে, এবা দেখতেঃ 192.168.1.0/28."

    return render(request, 'subnet_calculator.html', context)
