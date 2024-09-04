package com.Fancy.F3D;

import android.graphics.Bitmap;
import android.graphics.Color;
import android.graphics.drawable.BitmapDrawable;

import com.Fancy.Application.UIGlobal;

public class AndroidTextArea extends AndroidUI
{
	public int				mSize;
	public int				mAlign;
	public int				mTextColor;
	public boolean			mIsEditable;
	public BitmapDrawable	mImage;

	public void setEditable( boolean editable )
	{
		mIsEditable = editable;
		UIGlobal.sendMessage( this, UIGlobal.TEXTAREA_EDITABLE );
	}

	public void setText( String text )
	{
		mText = text;
		UIGlobal.sendMessage( this, UIGlobal.TEXTAREA_TEXT );
	}

	public String getText( )
	{
		return mText;
	}

	public void setTextSize( int size )
	{
		mSize = size;
		UIGlobal.sendMessage( this, UIGlobal.TEXTAREA_TEXTSIZE );
	}

	public void setTextColor( int color )
	{
		mTextColor = Color.rgb( ( color & 0xFF0000 ) >> 16, ( color & 0xFF00 ) >> 8, color & 0xFF );
		UIGlobal.sendMessage( this, UIGlobal.TEXTAREA_TEXTCOLOR );
	}

	public void setAlign( int align )
	{
		mAlign = align;
		UIGlobal.sendMessage( this, UIGlobal.TEXTAREA_ALIGN );
	}
	
	public void setImage( Bitmap name )
	{
		mImage = new BitmapDrawable( name );
		UIGlobal.sendMessage( this, UIGlobal.TEXTAREA_IMAGE );
	}

	public void removeView( )
	{
		UIGlobal.sendMessage( this, UIGlobal.TEXTAREA_REMOVE );
	}
}
