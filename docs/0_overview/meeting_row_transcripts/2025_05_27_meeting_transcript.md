Okay. We are trying to discuss.

2D Error Mapping Project. The requirement is. Capture the

Eras, occurred occurred. From the encoder and correct it Correct it using. Vision based correction system the errors, we Expecting due to the manufacturing defect from the encoder.

Construction time. Okay, the way we are trying to Correct is we are installed. Uh, camera overlooking glass scale which have One, millimetre and one millimetre dot grid. So that the location of the dot also, we also don't know. So so we created class scale certificate generation mechanism. So while by executing the class scale, Generation mechanism.

We we scanned. Consider 10 by 10. Ah dot grid and we capture multiple images overlooking at 2 2 or more images dots. So, we measure the distance between 2 dot, We measure the distance between dot dot and Accumulate the distance. All the way 0 0.210 and 10 dot. By 00.

0 by 0. To 10 by 10. Dot so, by doing so. We can measure the distance between 0, dot to 10 Dot and zero dot to the other side of the 10 dock and calculate the distance in physical. Device you right now, we are using lesser interferometer to measure.

So, by doing it, we can measure the distance in the accuracy of 100 nanometre. So we are we are we are confidence that we can measure the distance between two dots up to 100 nanometre. Also, we can capture the image. Uh, using the stitching multiple images together. We can measure the distance between dot 2 dot also.

The the stitching the scanning of the grid, Four image collection to generate. Generate. Glass certificate is done in. Uh, SRC back end. Src. Es SRC, backend image processing and scanned, and capture.py5. So that by executing the scan procedure, Related to Expansion, 2D expansion. We can we can measure the distance between dot two dots.

Then we, we perform the Perform our Performance service. The name is General 2D glass certificate. 2 0 7. So, That that service going through over the images we capture and generate the class certificate for us. Okay, so then after we

Then after we use that glass certificate and run, generate 2D encoder error Matrix which also in service services, Services fold. So we run that that file from that file, we we generate Errors based on. Based on Vision. And encoder error based on Vision values Vision based image. So we generate the certificate for the glass scale and we use the grass scale to generate the encoder error.

So Then after we try to test the system. So by the way, we try to test is the error, we have to feed back to the controller as As of buffer format. So we we use the by doing the by generating you by running executing January 2D encoder Matrix.

We are generating two, three files. Actually, the files name are X axis X error, map 2D CV, CSV, and Y error map, 2D CSV those two files are used to update the errors to the ACs controller so we can correct it, but but we have a certain limitations of doing the doing and testing the era.

So we are creating another set of files so that file is Ah, similar to the previous file, but similar to the to drama that file is 2D I generate 2T array map. Underscore test test.py. So in that file and that python program, where I try to generate a few different files.

The first file is We use the 2D array map. X axis the map. 2d CSV file and And we remove some rows and column values and generate x axis map, X error, map, 2D 4test.csv5 Ah, then we use Y error map, 2T CSV file and can remove some X columns, and rows and generate X Y error map.

2d4 test. Dot CSV file. So we use, we removing the original area map grid and using the part of that error map and we upload that one to Scs control, then we use the remaining the reef remaining part of the thing to test. So we know the values we are generated is correct by doing so.

So right now, I am trying to generate a test plot which are in Sasi backend Services. Generate 2D array map test, plot.p Wi-Fi So, in that file, I am trying to generate x directional error map and the y directional error map,

In here. The challenge is X directional. We can simply generate the drama but the y directional plot. We have to select the correct values because The way I save the data in the CSC file when I do the Test again. The way I saved the data is not suitable to not directly can use to plot the y directional.

Repeatability. So I need to refactor it.

So we use this data to use, please use this transcript, the meeting node, to generate the process flow for me. And the few diagrams. Uh, a few years few diagrams.