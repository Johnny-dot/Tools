package com.Fancy.F3D;

import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;

import com.Fancy.Application.UIGlobal;

public class AndroidSpin extends AndroidUI
{
	public BitmapDrawable mLeftUp;
	public BitmapDrawable mLeftDown;
	public BitmapDrawable mRightUp;
	public BitmapDrawable mRightDown;
	public BitmapDrawable mCenter;

	public void setText( String text )
	{
		mText = text;
		UIGlobal.sendMessage( this, UIGlobal.SPIN_VALUE );
	}

	public void setImage( Bitmap leftUp, Bitmap leftDown, Bitmap rightUp, Bitmap rightDown, Bitmap center )
	{
		mLeftUp = new BitmapDrawable( leftUp );
		mLeftDown = new BitmapDrawable( leftDown );
		mRightUp = new BitmapDrawable( rightUp );
		mRightDown = new BitmapDrawable( rightDown );
		mCenter = new BitmapDrawable( center );

		UIGlobal.sendMessage( this, UIGlobal.SPIN_IMAGE );
	}

	public void removeView( )
	{
		UIGlobal.sendMessage( this, UIGlobal.SPIN_REMOVE );
	}
}