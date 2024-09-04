package com.Fancy.F3D;

import android.graphics.Bitmap;
import android.graphics.Color;
import android.graphics.drawable.BitmapDrawable;

import com.Fancy.Application.UIGlobal;

public class AndroidTextInput extends AndroidUI
{
	public boolean			mIsSecure;
	public int				mTextSize;
	public int				mTextColor;
	public BitmapDrawable	mImage;

	public void setText( String text )
	{
		mText = text;
		UIGlobal.sendMessage( this, UIGlobal.EDIT_SET_TEXT );
	}

	public String getText( )
	{
		return mText;
	}

	public void setTextColor( int color )
	{
		mTextColor = Color.rgb( ( color & 0xFF0000 ) >> 16, ( color & 0xFF00 ) >> 8, color & 0xFF );
		UIGlobal.sendMessage( this, UIGlobal.EDIT_SET_TEXTCOLOR );
	}

	public void setTextSize( int size )
	{
		mTextSize = size;
		UIGlobal.sendMessage( this, UIGlobal.EDIT_SET_TEXTSIZE );
	}

	public void setSecure( boolean isSecure )
	{
		mIsSecure = isSecure;
		UIGlobal.sendMessage( this, UIGlobal.EDIT_PASSWORD );
	}

	public void setImage( Bitmap buffer )
	{
		mImage = new BitmapDrawable( buffer );
		UIGlobal.sendMessage( this, UIGlobal.EDIT_IMAGE );
	}
	
	public void removeView( )
	{
		UIGlobal.sendMessage( this, UIGlobal.EDIT_REMOVE );
	}
}