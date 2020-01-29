#!/bin/sh

sub=$1

echo "Processing " $sub

#############################
#############################
# lh whole

src=/home/stone/eshed/beta_bricks/new_rois/$sub/lh.VTC.mgz
dst=/home/stone-ext1/freesurfer/subjects/$sub/label/lhDENSETRUNCpt.VTC_anat.mgz

cp $src $dst

# rh whole

src=/home/stone/eshed/beta_bricks/new_rois/$sub/rh.VTC.mgz
dst=/home/stone-ext1/freesurfer/subjects/$sub/label/rhDENSETRUNCpt.VTC_anat.mgz

cp $src $dst

#############################
#############################
# lh lateral

src=/home/stone/eshed/beta_bricks/new_rois/$sub/lh.VTC_lateral.mgz
dst=/home/stone-ext1/freesurfer/subjects/$sub/label/lhDENSETRUNCpt.VTC_lateral.mgz

cp $src $dst

# rh lateral

src=/home/stone/eshed/beta_bricks/new_rois/$sub/rh.VTC_lateral.mgz
dst=/home/stone-ext1/freesurfer/subjects/$sub/label/rhDENSETRUNCpt.VTC_lateral.mgz

cp $src $dst

#############################
#############################
# lh medial

src=/home/stone/eshed/beta_bricks/new_rois/$sub/lh.VTC_medial.mgz
dst=/home/stone-ext1/freesurfer/subjects/$sub/label/lhDENSETRUNCpt.VTC_medial.mgz

cp $src $dst

# rh medial

src=/home/stone/eshed/beta_bricks/new_rois/$sub/rh.VTC_medial.mgz
dst=/home/stone-ext1/freesurfer/subjects/$sub/label/rhDENSETRUNCpt.VTC_medial.mgz

cp $src $dst
