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
