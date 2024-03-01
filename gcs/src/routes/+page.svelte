<script lang="ts">
	export const ssr = false;
	import { Canvas } from '@threlte/core';
	import Scene from './Scene.svelte';
	import { onMount } from 'svelte';
	import { dataStore } from '../stores';
	import Performance from '../components/Performance.svelte';
	import { PUBLIC_LOCAL_WS } from '$env/static/public';
	

	
	let count = 0;
	

	onMount(() => {
		const client = new WebSocket(PUBLIC_LOCAL_WS);

		client.addEventListener('message', (event) => {
			const data = JSON.parse(event.data);

			if (data.type === 'attitude') {
				dataStore.set(data);
			}
		});
	});

	let incoming = [];
</script>

<section class="p-5">
	<div class="">
		<div class="navbar rounded-md bg-primary">
			<a class="btn btn-ghost normal-case text-xl" href="">UAS@UCLA | Ground Control Station</a>
		</div>
	</div>

	<div class="grid-cols-2 grid">
		<div class="col-span-2">
			<p class="text-md mt-5 mb-2">Performance Metrics</p>
			<div class=" h-96 p-5 bg-primary rounded-md">
				<Performance Labels={[]} chartData={[]} />
			</div>
		</div>
		<div>
			<p class="text-md mt-5 mb-2">Live Orientation</p>
			<div class="w-96 h-96 bg-base-200 rounded-md">
				<Canvas>
					<Scene />
				</Canvas>
			</div>
		</div>
	</div>
</section>
