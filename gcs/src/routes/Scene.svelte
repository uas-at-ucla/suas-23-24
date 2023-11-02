<script>
	import { T, useFrame } from '@threlte/core';
	import { interactivity } from '@threlte/extras';
	import { spring } from 'svelte/motion';
	interactivity();
	const scale = spring(1);
	let rotation = 0;
	useFrame((state, delta) => {
		rotation += delta;
        console.log(rotation)
	});
</script>

<T.PerspectiveCamera
	makeDefault
	position={[10, 10, 10]}
	on:create={({ ref }) => {
		ref.lookAt(0, 1, 0);
	}}
/>

<T.DirectionalLight position={[0, 10, 10]} />

<T.Mesh
	rotation.y={rotation}
    rotation.x={rotation}
    rotation.z={rotation}
	position.y={1}
	scale={$scale}
	on:pointerenter={() => scale.set(4.5)}
	on:pointerleave={() => scale.set(4)}
>
	<T.BoxGeometry args={[1, 2, 1]} />
	<T.MeshStandardMaterial color="hotpink" />
</T.Mesh>
