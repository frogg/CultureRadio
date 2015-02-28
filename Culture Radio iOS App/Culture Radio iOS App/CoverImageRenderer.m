//
//  CoverImageRenderer.m
//  Culture Radio iOS App
//
//  Created by Frederik Riedel on 27.02.15.
//  Copyright (c) 2015 Frederik Riedel. All rights reserved.
//

#import "CoverImageRenderer.h"

@implementation CoverImageRenderer



+(void) renderCoverImageForLocation:(MKCoordinateRegion) region withLocationName:(NSString *) locationName forBandName:(NSString *) bandName usingCoverImage:(UIImage *) coverImage andCallbackBlock:(void (^)(UIImage *))block {
    UIView *view = [[UIView alloc] initWithFrame:CGRectMake(0, 0, 400, 400)];
    
    
    
    
    dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
        
        
        MKMapSnapshotOptions *options = [[MKMapSnapshotOptions alloc] init];
        options.region = region;
        options.size = view.frame.size;
        options.mapType=MKMapTypeHybrid;
        options.scale = [[UIScreen mainScreen] scale];
        
        
        MKMapSnapshotter *snapshotter = [[MKMapSnapshotter alloc] initWithOptions:options];
        [snapshotter startWithCompletionHandler:^(MKMapSnapshot *snapshot, NSError *error) {
            if (error) {
                NSLog(@"[Error] %@", error);
                return;
            }
            
            UIImage *image = snapshot.image;
            
            UIImageView *mapImageView = [[UIImageView alloc] initWithFrame:view.frame];
            mapImageView.image=image;
            [view addSubview:mapImageView];
            
            
            UIImageView *coverStecknadelImageView = [[UIImageView alloc] initWithFrame:CGRectMake(100, 100, 200, 200)];
            coverStecknadelImageView.image=[UIImage imageNamed:@"coverStecknadel.png"];
            [view addSubview:coverStecknadelImageView];
            
            UIImageView *coverImageView = [[UIImageView alloc] initWithFrame:CGRectMake(110, 105, 180, 150)];
            coverImageView.image=coverImage;
            coverImageView.layer.cornerRadius=10;
            coverImageView.clipsToBounds=YES;
            coverImageView.contentMode=UIViewContentModeScaleAspectFill;
            [view addSubview:coverImageView];
            
            
            
            
            UIGraphicsBeginImageContextWithOptions(view.bounds.size, NO, [UIScreen mainScreen].scale);
            
            [view drawViewHierarchyInRect:view.bounds afterScreenUpdates:YES];
            
            UIImage *result = UIGraphicsGetImageFromCurrentImageContext();
            UIGraphicsEndImageContext();
            
            dispatch_async(dispatch_get_main_queue(), ^{
                block(result);
            });
        }];
    });
    
    
}



@end
