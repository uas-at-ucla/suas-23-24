<script lang="ts">
	import { T, useFrame } from '@threlte/core';
	import { interactivity } from '@threlte/extras';
	import { spring } from 'svelte/motion';
	import { get } from 'svelte/store';
	import { dataStore } from '../stores';
	import { lerp } from 'three/src/math/MathUtils.js';
	import type { LocationUpdatePayload } from '../types';

	interactivity();
	const scale = spring(1);

	let data: LocationUpdatePayload = {};
	dataStore.subscribe((newData) => {
		data = newData;
	});

	let smoothData: LocationUpdatePayload = { ...data };
	useFrame(() => {
		smoothData.x = lerp(smoothData.x || 0, data.x || 0, 0.05);
		smoothData.y = lerp(smoothData.y || 0, data.y || 0, 0.05);
		smoothData.z = lerp(smoothData.z || 0, data.z || 0, 0.05);

	});
</script>


<T.PerspectiveCamera
	makeDefault
	position={[10, 10, 10]}
	on:create={({ ref }) => {
		ref.lookAt(0, 0, 0);
	}}
/>

<T.DirectionalLight position={[0, 10, 10]} />

<T.Mesh
	rotation.x={smoothData.x}
	position.y={smoothData.y}
	rotation.z={smoothData.z}
	scale={$scale}
	on:pointerenter={() => scale.set(4.5)}
	on:pointerleave={() => scale.set(4)}
>
	<T.BoxGeometry args={[1, 1, 1]} />
	<T.MeshStandardMaterial color="red" />
</T.Mesh>
