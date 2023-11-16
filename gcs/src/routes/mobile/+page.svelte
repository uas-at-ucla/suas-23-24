<script lang="ts">
	import { onMount } from 'svelte';

	let ws: WebSocket;

	onMount(() => {
		ws = new WebSocket('ws://100.116.136.106:8001');
		ws.onopen = () => console.log('ws opened');
		ws.onclose = () => console.log('ws closed');
	});

	let x = 0;
	let y = 0;
	let z = 0;

	function sendUpdate() {
		console.log(x, y, z);
		ws.send(
			JSON.stringify({
				type: 'location_update',
				altitude: -0.023536746958252586,
				latitude: -0.15615549651528826,
				longitude: 0.007802551109168601,
				heading: 179.60099524558524,
                x: x,
                y: y,
                z: z,
			})
		);
	}
</script>

<input
	type="range"
	min="-3.14159"
	max="3.14159"
	step="0.01"
	bind:value={x}
	on:input={sendUpdate}
/>
<input
	type="range"
	min="-3.14159"
	max="3.14159"
	step="0.01"
	bind:value={y}
	on:input={sendUpdate}
/>
<input
	type="range"
	min="-3.14159"
	max="3.14159"
	step="0.01"
	bind:value={z}
	on:input={sendUpdate}
/>
