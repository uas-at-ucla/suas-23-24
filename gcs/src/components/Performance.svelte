<script>
	import { Chart, BarController, CategoryScale, LinearScale, BarElement } from 'chart.js';
	import { onMount } from 'svelte';

	Chart.register(BarController, CategoryScale, LinearScale, BarElement);

	export let chartData = [20, 100, 50, 12, 20, 130, 45];
	export let Labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' ];
	let ctx;
	/**
	 * @type {HTMLCanvasElement}
	 */
	let chartCanvas;

	onMount(async () => {
		  ctx = chartCanvas.getContext('2d');
			// @ts-ignore
			var chart = new Chart(ctx, {
				type: 'bar',
				data: {
					labels: Labels,
					datasets: [{
							label: 'Unit Sales',
							data: chartData
					}]
				},
				options: {
					scales: {
						x: {
							type: 'category',
						},
						y: {
							type: 'linear',
						}
					}
				}
		});

	});
</script>
<canvas bind:this={chartCanvas} id="myChart"></canvas>