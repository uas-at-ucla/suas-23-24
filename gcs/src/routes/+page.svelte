<script lang="ts">
	import { Canvas } from '@threlte/core';
	import Scene from './Scene.svelte';
</script>

<section class="p-5">
	<div class="">
		<div class="navbar rounded-md bg-primary">
			<a class="btn btn-ghost normal-case text-xl">UAS@UCLA | Ground Control Station</a>
		</div>
	</div>

	<p class="text-md mt-5 mb-2">Live Orientation</p>
	<div class="w-96 h-96 bg-base-200 rounded-md">
		<Canvas>
			<Scene />
		</Canvas>
	</div>
</section>
