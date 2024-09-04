package com.Fancy.F3D;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;

import com.Fancy.Application.UIGlobal;
import com.Fancy.Application.VideoView;

import android.media.AudioManager;
import android.media.MediaPlayer;
import android.media.MediaPlayer.OnPreparedListener;
import android.view.View;

public class AndroidVideo
{
	public MediaPlayer			mMediaPlayer;
	public String				mFileName;
	public boolean				mFill;
	private int					mState;
	private FileInputStream		mFileStream;
	private boolean				mIsDone;
	public void CreateAndroidVideo( String name )
	{
		mFill = false;
		mFileName = name;
		mState = 0;
		mIsDone = false;
		UIGlobal.sendMessage( this, UIGlobal.VIDEO );
	}

	public void createMediaPlayer( )
	{
		mMediaPlayer = new MediaPlayer();
		try {
			if ( mFileStream != null )
				mFileStream.close( );
		} catch (IOException e2) {
			// TODO Auto-generated catch block
			e2.printStackTrace();
			mState = 2;
			mMediaPlayer = null;
			return;
		}

		try {
			mFileStream = UIGlobal.active.openFileInput( mFileName );
		} catch (FileNotFoundException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
			mState = 2;
			mMediaPlayer = null;
			return;
		}
 
		if ( mFileStream == null )
		{
			System.out.println("Load video file : " + mFileName + " faild!");
			mState = 2;
			mMediaPlayer = null;
			return;
		}

		try {
			mMediaPlayer.setDataSource( mFileStream.getFD( ) );
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			mState = 2;
			mMediaPlayer = null;
			return;
		}

		System.out.println("Load video file : " + " Done!");
		try {
			mMediaPlayer.setAudioStreamType(AudioManager.STREAM_MUSIC); 
		} catch (NullPointerException e) {
			mState = 2;
			mMediaPlayer = null;
			return;
		}

		try
		{
			System.out.println("prepareAsync , being");
			mMediaPlayer.setOnPreparedListener(new OnPreparedListener() 
			{
				public void onPrepared(MediaPlayer mp) 
				{
					System.out.println("onPrepared , onPrepared");
					//mMediaPlayer.seekTo( 0 );
					((VideoView)UIGlobal.videoview).waitHolder(mMediaPlayer);
					mState = 1;
				}
			});
    		mMediaPlayer.prepareAsync();

		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			mState = 2;
			mMediaPlayer = null;
			return;
		}

		mMediaPlayer.setOnCompletionListener( new MediaPlayer.OnCompletionListener( ) 
		{
				@Override
				public void onCompletion( MediaPlayer mediaPlayer )
	 			{
					mIsDone = true;
					UIGlobal.glView.setVisibility( View.VISIBLE );
					UIGlobal.videoview.setVisibility( View.GONE );
               }
          });
	}
	
	
	public boolean isPlaying( )
	{
		if ( mMediaPlayer != null )
			return mMediaPlayer.isPlaying( );
		return false;
	}

	public int getDuration( )
	{
		if ( mMediaPlayer != null )
			return mMediaPlayer.getDuration( );

		return 0;
	}

	public int getCurrentTime( )
	{
		if ( mMediaPlayer == null )
			return 0;
		else if ( mIsDone  )
			return mMediaPlayer.getDuration( );
		else
			return mMediaPlayer.getCurrentPosition( );
	}

	public void pause( )
	{
		if ( mMediaPlayer != null )
			UIGlobal.sendMessage( this, UIGlobal.VIDEO_PAUSE );
	}

	public void play( boolean fill )
	{
		mFill = fill;

		if ( mMediaPlayer == null )
			return;

		if ( mIsDone == true )
		{
			mMediaPlayer.stop( );
			mMediaPlayer.prepareAsync();
		}

		UIGlobal.sendMessage( this, UIGlobal.VIDEO_PLAY );
	}

	public void stop( )
	{
		if ( mMediaPlayer == null )
			return;

		UIGlobal.sendMessage( this, UIGlobal.VIDEO_STOP );
	}

	public void setDone( boolean done )
	{
		mIsDone = done;
	}
	
	public boolean getDone( )
	{
		return  mIsDone;
	}

	public int getState( )
	{
		return mState;
	}

	public void release( )
	{
		mState = 2;
		if ( mMediaPlayer == null )
			return;

		try {
			mFileStream.close( );
		} catch (IOException e2) {
			// TODO Auto-generated catch block
			e2.printStackTrace();
		}
	}
}