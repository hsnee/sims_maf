#!/bin/tcsh

## This script will generate AND RUN the command to concatenate mp4 files generated as movies
## of each individual opsim night.
## It uses ffmpeg: ffmpeg will concatenate the files included in the file 'tmpMovieList'
## Note that the tmpMovieList file consists of a line pointing to the mp4 file, then another pointing to
##  a special "blank.mp4" file, which is part of the git repo. The 'blank.mp4' file places a short
##  blank space between each movie night. Adding more versions of 'blank.mp4' will add a longer pause.
## Note that the tmpMovieList file could be edited and the ffmpeg command rerun to change these pauses, etc.

## usage: expects to be run after mkOpsMovie.sh is used to generate movies for a series of individual nights.
## usage: joinOpsMovie.sh [db name] [start night] [end night]

set opsRun = $1
set nightStart = $2
set nightEnd = $3
echo "#Joining movie from " $opsRun " for nights " $nightStart " to " $nightEnd

set nights = `seq $nightStart $nightEnd`
set movieList = 'tmpMovieList'
if (-e $movieList) then
   rm $movieList
   endif
foreach night ( $nights )
 if (-e $opsRun"_n"$night"/movieFrame_SkyMap_30.0_30.0.mp4") then
    echo "file "$opsRun"_n"$night"/movieFrame_SkyMap_30.0_30.0.mp4" >> $movieList
    echo "file blank.mp4" >> $movieList
 endif
 end

echo "ffmpeg -f concat -i "$movieList" -c copy "$opsRun"_n"$nightStart"_n"$nightEnd".mp4"
ffmpeg -f concat -i "$movieList" -c copy "$opsRun"_n"$nightStart"_n"$nightEnd".mp4
