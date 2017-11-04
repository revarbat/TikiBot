use <BOSL/transforms.scad>
use <BOSL/shapes.scad>
use <BOSL/joiners.scad>


/* [General] */

// Which part to print.
parts = "feedguide"; // [assembled:Full Assembly,feedguide:Output Feed Guide,ringseg:Ring Segment,stand:Standoff Pillars]

// Thickness of walls in mm.
wall_thick = 5; // [2:0.5:10]

// Number of pumps in the ring.
pump_count = 12; // [4:1:24]

tubing_diam = 9;

stand_height = 200;


/* [Pump] */

// Diameter of pump body, in mm.
pump_diam = 27.5; // [20:0.5:75]

// Diameter of pump inlet, in mm.
pump_inlet_diam = 8; // [3:0.5:10]

// Diameter of pump outlet, in mm.
pump_outlet_diam = 8; // [3:0.5:10]

// Offset of pump outlet, in mm.
pump_outlet_offset = 9.5; // [3:0.5:35]

// Offset of pump outlet, in mm.
pump_outlet_angle = 0; // [0:15:345]

// Length of pump, in mm.
pump_length = 61.0; // [20:0.5:100]

// Size of pump screws in mm.
pump_screw_size = 2.0; // [2:5]

// Size of pump screws in mm.
pump_screw_spacing = 32.0; // [20:0.5:75]


/* [Valve] */

// Diameter of valve body, in mm.
valve_diam = 24; // [16:0.5:75]

// Diameter of valve inlet, in mm.
valve_inlet_diam = 8; // [3:0.5:10]

// Diameter of valve outlet, in mm.
valve_outlet_diam = 8; // [3:0.5:10]

// Offset of valve outlet, in mm.
valve_outlet_offset = 9.5; // [3:0.5:35]

// Offset of valve outlet, in mm.
valve_outlet_angle = 0; // [0:15:345]

// Length of valve, in mm.
valve_length = 37.0; // [20:0.5:100]




/* [Hidden] */

pi = 3.141592653589793236;

slop = 0.2;


$fa = 3;
$fs = 3;


wedge_height = max(pump_length, valve_length) + wall_thick + 10;
wedge_width = max(pump_diam, valve_diam) - wall_thick;
wedge_depth = pump_diam+valve_diam+3*wall_thick;

module pump_housing_ring_segment()
{
	h = wedge_height;
	w = wedge_width;
	d = wedge_depth;
	ow = w + d * 2 * tan(360/pump_count/2);
	joiner_height = h * 0.75;
	union() {
		difference() {
			union() {
				// Main wedge shape.
				up(h/2) xrot(-90) trapezoid([w, h], [ow, h], h=d, center=true);

				// Feed guide support
				up(10+2+1) fwd(d/2) trapezoid([10, 0.1], [10, 2*4], h=6, center=false);
			}

			// side joiner clearing
			up(joiner_height/2) {
				yrot_copies([0, 180]) {
					right(w/2) {
						fwd(d/2) {
							zrot(-360/pump_count/2) {
								back(d/2-wall_thick/2) {
									zrot(90) joiner_clear(h=joiner_height, w=8, clearance=1);
									back(d/2-wall_thick) zrot(-90) yrot(180) joiner_clear(h=joiner_height, w=8, clearance=1);
								}
							}
						}
					}
				}
			}

			// radial wiring holes
			up(2) upcube([valve_diam-2*3, d+1, 10], center=true);

			// Pump hole
			back(d/2-pump_diam/2-wall_thick) {
				// Diametral wiring holes
				up(2) {
					xflip_copy() {
						zrot(360/pump_count/2) {
							left(ow/2) upcube([ow, pump_diam/2, 10]);
							left(pump_diam/2-4) {
								up(10-0.01) trapezoid([2*3, pump_diam/2], [0.1, pump_diam/2], h=5, center=false);
							}
						}
					}
				}

				// radial wiring hole taper
				up(10+2-0.01) trapezoid([valve_diam-2*3, pump_diam-2], [valve_diam-2*3, pump_diam-2*5], h=5, center=false);

				// Pump Body hole
				up(h-pump_length+0.01) {
					cylinder(h=pump_length, d=pump_diam, center=false);
					cylinder(h=h*3, d=pump_diam-3, center=true);
				}

				// Pump Tabs
				up(h-2+0.01) {
					xspread(pump_screw_spacing) {
						upcube([pump_screw_size*2.5, pump_screw_size*2.5, 2]);
					}
				}

				// Pump tab screw holes
				up(h-15+0.01) {
					xspread(pump_screw_spacing) {
						cylinder(d=pump_screw_size, h=16, center=false);
					}
				}
			}

			// Valve hole
			fwd(d/2-valve_diam/2-wall_thick) {
				// Valve body hole and shelf.
				up(h-valve_length+0.01) cylinder(h=valve_length, d=valve_diam, center=false);
				down(0.01) trapezoid([valve_diam-8, 10], [valve_diam-2, 8], h=h-valve_length+1, center=false);

				// Valve output clearance
				up(h-valve_outlet_diam/2) {
					up(5/2) {
						hull() {
							zspread(5) {
								xrot(90) cylinder(d=valve_outlet_diam, h=valve_diam, center=false);
							}
						}
					}
				}
			}
		}

		// Side Joiners
		up(joiner_height/2) {
			yrot_copies([0,180]) {
				right(w/2) {
					fwd(d/2) {
						zrot(-360/pump_count/2) {
							back(d/2-wall_thick/2) {
								zrot(-90) joiner(h=joiner_height, w=8, l=6);
								back(d/2-wall_thick) zrot(-90) yrot(180) joiner(h=joiner_height, w=8, l=6, slop=slop);
							}
						}
					}
				}
			}
		}
	}
}
//!pump_housing_ring_segment();



module pump_housing_feed_guide()
{
	h = 15;
	w = wedge_width;
	d = wedge_depth;
	funnel_diam = 75;
	r = w / 2 / sin(180/pump_count);
	difference() {
		// Main body.
		cylinder(r=r, h=h, center=false, $fn=pump_count);

		// Central stacking bank bypass.
		cylinder(d=tubing_diam*1.75, h=h*3, center=true);

		// Inner ring of feeds.
		zring(n=pump_count/2, r=tubing_diam*2.0) {
			yrot(-10) xrot(-15) cylinder(d=tubing_diam, h=h*3, center=true);
		}

		// Outer ring of feeds.
		zrot(360/(pump_count/2)/2) {
			zring(n=pump_count/2, r=tubing_diam*3.0) {
				yrot(-10) xrot(-20) cylinder(d=tubing_diam, h=h*3, center=true);
			}
		}

		// funnel groove
		hull() {
			grid_of(xa=[0, 2*r]) {
				up(h-2) {
					cylinder(h=1.01, d=funnel_diam, center=false);
					up(1) cylinder(h=1.01, d1=funnel_diam, d2=funnel_diam-2*1, center=false);
				}
			}
		}
	}
}



module pump_housing_stand()
{
	h = stand_height * ((stand_height>150)? 0.5 : 1.0);
	w = wedge_width;
	d = wedge_depth;
	joiner_height = h * 0.75;
	union() {
		difference() {
			union() {
				cylinder(h=h, d=pump_diam+6, center=false);
				cylinder(h=h+12, d=pump_diam-3-slop, center=false);
			}
			down(0.01) {
				cylinder(h=h*2, d=pump_diam-10, center=false);
				difference() {
					cylinder(h=h-10+0.02, d=pump_diam-3, center=false);
					upcube([10-slop, d, 10-slop]);
				}
				up(h-10) {
					cylinder(h=7, d1=pump_diam-3, d2=pump_diam-10, center=false);
				}
			}
			up(10/2-0.01) {
				xrot(-90) upcube([10, 10, d]);
			}
			up(h) {
				upcube([10-slop, d, 20]);
			}
		}
	}
}



module pump_housing_parts() { // make me
	h = wedge_height;
	w = wedge_width;
	d = wedge_depth;
	r = w / 2 / sin(180/pump_count) + d/2;
	if (parts == "assembled") {
		zring(r=r, n=pump_count, rot=true) {
			zrot(-90) pump_housing_ring_segment();
		}
		up(22+10+2+1) {
			zrot(360/pump_count/2) yrot(180) pump_housing_feed_guide();
		}
	} else if (parts == "ringseg") {
		pump_housing_ring_segment();
	} else if (parts == "feedguide") {
		pump_housing_feed_guide();
	} else if (parts == "stand") {
		pump_housing_stand();
	}
}



pump_housing_parts();



// vim: noexpandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap

