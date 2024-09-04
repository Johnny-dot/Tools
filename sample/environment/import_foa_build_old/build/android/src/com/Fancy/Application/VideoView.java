package com.Fancy.Application;

import android.content.Context;
import android.media.MediaPlayer;
import android.view.MotionEvent;
import android.view.SurfaceHolder;
import android.view.SurfaceView;

public class VideoView extends SurfaceView
{
	public boolean hasActiveHolder = false;
	private MediaPlayer mPlayer;
	private boolean mIsPlaying;
	private int mCurrentPosition;

	public VideoView( Context context )
	{
		super( context );

		mCurrentPosition = 0;
		mIsPlaying = false;
		final VideoView view = this;
		this.getHolder( ).addCallback( new SurfaceHolder.Callback( )
		{
			@Override
			public void surfaceCreated( SurfaceHolder holder )
			{
				view.hasActiveHolder = true;

				if ( mPlayer != null )
					mPlayer.setDisplay( holder );

				if ( mCurrentPosition > 0 )
				{
					mPlayer.seekTo( mCurrentPosition );
					mPlayer.start( );
					mCurrentPosition = 0;
				}
			}

			@Override
			public void surfaceDestroyed( SurfaceHolder holder )
			{
				if ( mPlayer != null )
					mCurrentPosition = mPlayer.getCurrentPosition( );

				hasActiveHolder = false;
			}

			@Override
			public void surfaceChanged( SurfaceHolder holder, int format, int width, int height ) { }
		});
	}

	@Override
	public boolean onCheckIsTextEditor( )  
	{
		return true;
	}

	@Override
	public boolean onTouchEvent( MotionEvent event )
	{
		return UIGlobal.glView.onTouchEvent( event );
	}
	
	public void waitHolder( MediaPlayer player )
	{
		if( hasActiveHolder )
			player.setDisplay( this.getHolder( ) );
		else
			mPlayer = player;
	}

	public void pause( )
	{
		if ( hasActiveHolder == false || mPlayer == null || mCurrentPosition > 0 )
			return;

		mPlayer.pause( );
	}

	public void resume( )
	{
		if ( hasActiveHolder == false || mPlayer == null || mCurrentPosition > 0 )
			return;

		mPlayer.start( );
	}
}