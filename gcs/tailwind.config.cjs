const daisyui = require('daisyui');

/** @type {import('tailwindcss').Config}*/
const config = {
	content: ['./src/**/*.{html,js,svelte,ts}'],

	daisyui: {
		themes: [
			{
				uas: {
					primary: '#2274AE',

					secondary: '#FFD100',

					accent: '#FFC72C',

					neutral: '#272626',

					'base-100': '#003B5C',

					info: '#0000ff',

					success: '#00FF87',

					warning: '#ffff00',

					error: '#ff0000'
				}
			},
			"black"
		]
	},

	theme: {
		extend: {}
	},

	plugins: [daisyui]
};

module.exports = config;
