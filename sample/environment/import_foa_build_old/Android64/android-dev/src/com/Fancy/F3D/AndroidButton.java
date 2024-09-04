package com.Fancy.F3D;

import com.Fancy.Application.UIGlobal;

import android.graphics.Bitmap;
import android.graphics.Color;
import android.graphics.drawable.BitmapDrawable;

public class AndroidButton extends AndroidUI
{
	public int				mTitleSize;
	public int				mTitleColor;
	public int				mBackColor;
	public BitmapDrawable	mNormalImage;
	public BitmapDrawable	mClickImage;
	public BitmapDrawable	mDisabledImage;

	public void setText( String text )
	{
		mText = text;
		UIGlobal.sendMessage( this, UIGlobal.BUTTON_TITLE );
	}

	public void setTextColor( int color )
	{
		mTitleColor = Color.rgb( ( color & 0xFF0000 ) >> 16, ( color & 0xFF00 ) >> 8, color & 0xFF );
		UIGlobal.sendMessage( this, UIGlobal.BUTTON_TITLE_COLOR );
	}

	public void setTextSize( int size )
	{
		mTitleSize = size;
		UIGlobal.sendMessage( this, UIGlobal.BUTTON_TITLE_SIZE );
	}

	public void setImage( Bitmap normal, Bitmap click, Bitmap disabled )
	{
		mNormalImage = new BitmapDrawable( normal );
		mClickImage = new BitmapDrawable( click );
		mDisabledImage = new BitmapDrawable( disabled );

		UIGlobal.sendMessage( this, UIGlobal.BUTTON_IMAGE );
	}

	public void setBgColor( int color )
	{
		mBackColor = Color.rgb( ( color & 0xFF0000 ) >> 16, ( color & 0xFF00 ) >> 8, color & 0xFF );
		UIGlobal.sendMessage( this, UIGlobal.BUTTON_BACKGROUND_COLOR );
	}
	
	public void removeView( )
	{
		UIGlobal.sendMessage( this, UIGlobal.BUTTON_REMOVE );
	}
}