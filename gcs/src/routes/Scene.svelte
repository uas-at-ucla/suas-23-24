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

	let scaleValue = 1;
	let isIncreasing = true;

	let offset = 0;

	export function evaluateOffset() {
		console.log('calced');
		if (data.orientation.yaw) offset = data.orientation.yaw;
	}

	setInterval(() => {
		if (isIncreasing) {
			scaleValue += 0.1;
		} else {
			scaleValue -= 0.1;
		}

		if (scaleValue >= 1.5) {
			isIncreasing = false;
		} else if (scaleValue <= 0) {
			isIncreasing = true;
		}
	}, 100);

	let data: LocationUpdatePayload = {
		orientation: {
			pitch: 0,
			roll: 0,
			yaw: 0
		},
		GPS: {}
	};
	dataStore.subscribe((newData) => {
		if (newData.orientation) {
			data = newData;
		}
	});

	let smoothData: LocationUpdatePayload = { ...data };
	useFrame(() => {
		smoothData.orientation.roll = lerp(
			smoothData.orientation.roll || 0,
			data.orientation.roll || 0,
			0.05
		);
		smoothData.orientation.pitch = lerp(
			smoothData.orientation.pitch || 0,
			data.orientation.pitch || 0,
			0.05
		);
		smoothData.orientation.yaw = lerp(
			smoothData.orientation.yaw || 0,
			data.orientation.yaw || 0,
			0.05
		);
	});
</script>

<T.PerspectiveCamera
	makeDefault
	position={[0, 5, 20]}
	on:create={({ ref }) => {
		ref.lookAt(0, 0, 0);
	}}
/>

<T.DirectionalLight position={[0, 10, 10]} />

<T.Mesh
	rotation.x={data.orientation.pitch}
	rotation.y={Math.PI / 2 - (data.orientation.yaw - offset)}
	rotation.z={-data.orientation.roll}
	on:click={() => {
		evaluateOffset();
	}}
>
	<T.BoxGeometry args={[3, 3, 3]} />
	<T.MeshStandardMaterial color="red" />
</T.Mesh>
