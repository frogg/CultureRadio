//
//  CoverImageRenderer.h
//  Culture Radio iOS App
//
//  Created by Frederik Riedel on 27.02.15.
//  Copyright (c) 2015 Frederik Riedel. All rights reserved.
//

@import UIKit;
@import CoreLocation;
@import MapKit;


@interface CoverImageRenderer : NSObject

+(void) renderCoverImageForLocation:(MKCoordinateRegion) region withLocationName:(NSString *) locationName forBandName:(NSString *) bandName usingCoverImage:(UIImage *) coverImage andCallbackBlock:(void (^)(UIImage *))block;

@end
