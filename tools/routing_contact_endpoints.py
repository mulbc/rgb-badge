# SPDX-License-Identifier: Apache-2.0
"""Additional endpoint centres whose round caps overlap an existing track cap."""
import math

def end_cap_points(start,end,old_width,new_width,overlap=5000):
 if old_width<=0 or new_width<=0 or not 0<overlap<(old_width+new_width)/2:
  raise ValueError('Positive widths and overlap inside the combined radii required')
 dx,dy=end[0]-start[0],end[1]-start[1];length=math.hypot(dx,dy)
 if not length:return []
 reach=(old_width+new_width)/2-overlap
 return [(round(start[0]-dx*reach/length),round(start[1]-dy*reach/length)),(round(end[0]+dx*reach/length),round(end[1]+dy*reach/length))]
