from django.shortcuts import render
from .models import SubnetCalculation
import ipaddress

# this make prefix to binary
def prefix_to_binary_mask(prefix_len):
    bits = '1' * prefix_len + '0' * (32 - prefix_len)
    return '.'.join(bits[i:i+8] for i in range(0, 32, 8))



def subnet_calculator(request):
    context = {} # this stands to send data to html

    if request.method == 'POST':
        cidr_input = request.POST.get('cidr_input') # This collect what user haven put into the cidr_input box on html

        if '/' not in cidr_input: #this stands for validate is this cidr formate or not
            # and these returns error regarding input 
            context['error'] = " হালার-পু খালি IP address দেস কেন, CIDR format দে — যেমন: 192.168.1.0/24"
            return render(request, 'subnet_calculator.html', context)
        
        try: 
            # this do core calculatioln
            network = ipaddress.ip_network(cidr_input, strict=False)
            
            if network.prefixlen < 10:
                context['error'] = "CIDR মানটা ছোট দে হালা (/<10) — এত বড় রেঞ্জ দিলে সার্ভার মারা খেয়ে যায়।"
                return render(request, 'subnet_calculator.html', context)


            subnet_mask = str(network.netmask)
            total_ip = network.num_addresses            
            usable_host = total_ip if network.prefixlen >= 31 else total_ip - 2            
            network_address = str(network.network_address)
            broadcast_address = str(network.broadcast_address)

            if usable_host == 0:
                first_host = last_host = None
            elif usable_host == total_ip:
                first_host = str(network.network_address)
                last_host = str(network.broadcast_address)
            else:
                first_host = str(network.network_address + 1) if usable_host > 0 else None
                last_host = str(network.broadcast_address - 1) if usable_host > 0 else None

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
