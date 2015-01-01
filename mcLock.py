import time
import sys

lock_prefix = "mc_lock_"

free_lock_time = 5 #second

class mcLock:
    def __init__( this , mc , name ):
        this.mc = mc 
        this.name = name
        this.isLock = False
        #this.conn = Client(("localhost" , 11212))

    def lock( this ):
        while True:
            if( this.mc.add( lock_prefix + this.name , 1 ) ):
                this.mc.set( lock_prefix + this.name + "_recent_time" , time.time() )
                this.isLock = True
                break
            else:
                recent_time = this.mc.get( lock_prefix + this.name + "_recent_time" )
                if time.time() - recent_time > free_lock_time:
                    this.unlock()
                time.sleep(0.01)

    def unlock( this ):
        this.isLock = False
        this.mc.delete( lock_prefix + this.name )

    def set( this , key , data , _time = 0 ):
        if this.isLock:
            this.mc.set( lock_prefix + this.name + "_recent_time" , time.time() )
        return this.mc.set( key , data , _time )

    def get( this , key ):
        if this.isLock:
            this.mc.set( lock_prefix + this.name + "_recent_time" , time.time() )
        return this.mc.get( key )

    def add( this , key , data , _time = 0 ):
        if this.isLock:
            this.mc.set( lock_prefix + this.name + "_recent_time" , time.time() )
        return this.mc.add( key , data , _time )

    def delete( this , key , _time = 0):
        if this.isLock:
            this.mc.set( lock_prefix + this.name + "_recent_time" , time.time() )
        return this.mc.delete( key , _time )


