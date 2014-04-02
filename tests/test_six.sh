balancer_addr=138.251.206.64
balancer_port=5000

printf '\nRunning producers: 4000 - 4015.\n'
for i in {4000..4015}
do
	printf 'Running producer %s.\n' "$i"
	python ../client/producer.py $balancer_addr $balancer_port $i &
done

function kill_all() {
	kill $(ps aux | grep '[p]ython ../client/producer.py' | awk '{print $2}')
}

trap "kill_all()" SIGINT
wait