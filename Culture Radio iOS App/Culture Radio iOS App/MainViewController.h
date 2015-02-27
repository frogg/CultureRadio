//
//  ViewController.h
//  Culture Radio iOS App
//
//  Created by Frederik Riedel on 27.02.15.
//  Copyright (c) 2015 Frederik Riedel. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "Config.h"
#import <Spotify/Spotify.h>
@import AVFoundation;
@import MediaPlayer;

@interface MainViewController : UIViewController


-(void)handleNewSession:(SPTSession *)session;

@end

