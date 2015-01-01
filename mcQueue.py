import mcLock
import time

#The lock is temporary, so the lock should be unlock after a moment.

class mcQueue:
    
    def __init__(this , mc , name , maxVolume = 2**32 - 1):
        this.name = name
        this.index_name = "mc_queue_" + name +"_index_"
        this.mcQueue_top = "mc_queue_top_" + name
        this.mcQueue_tail =  "mc_queue_tail_" + name
        this.mcQueue_lock = "mc_queue_" + name
        this.mc = mcLock.mcLock( mc , this.mcQueue_lock )
        this.maxVolume = maxVolume + 1

        #initialize mc
        this.mc.add( this.mcQueue_top , 0 )
        this.mc.add( this.mcQueue_tail , 0 )

    def isEmpty(this):
        try:
            ret = this.mc.get( this.mcQueue_top ) == this.mc.get( this.mcQueue_tail )
            return ret
        except Exception , e:
            print e
            return True


    def getSize(this):
        try:
            topindex = this.mc.get( this.mcQueue_top )
            tailindex = this.mc.get( this.mcQueue_tail )
            if topindex == None or tailindex == None:
                return -1
            size = (tailindex - topindex + this.maxVolume) % this.maxVolume
            return size
        except Exception , e:
            print e
            return -1


    def getTopIndex(this):
        try:
            index = this.mc.get( this.mcQueue_top )
            if index == None : index = -1
            return index
        except Exception , e:
            print e
            return -1


    def getTailIndex(this):
        try:
            index = this.mc.get( this.mcQueue_tail )
            if index == None : index = -1
            return index
        except Exception , e:
            print e
            return -1


    def getTop(this):
        try:
            topindex = this.mc.get( this.mcQueue_top )
            if topindex == None:
                return None
            topindex = ( topindex + 1 ) % this.maxVolume
            ret = this.mc.get( this.index_name + str(topindex) )
            return ret
        except Exception , e:
            print e
            return None


    def getTail(this):
        try:
            tailindex = this.mc.get( this.mcQueue_tail )
            if tailindex == None:
                return None
            ret = this.mc.get( this.index_name + str(tailindex) )
            return ret
        except Exception , e:
            print e
            return None


    def push(this , val):
        try:
            this.mc.lock()
            topindex = this.mc.get( this.mcQueue_top )
            tailindex = this.mc.get( this.mcQueue_tail )
            if topindex == None or tailindex == None:
                return False
            tailindex = ( tailindex + 1 ) % this.maxVolume
            if( topindex == tailindex ):
                this.mc.unlock()
                return False
            else:
                this.mc.set( this.mcQueue_tail , tailindex )
                this.mc.set( this.index_name + str(tailindex) , val )
            this.mc.unlock()
            return True
        except Exception , e:
            print e
            this.mc.unlock()
            return False    


    def pop(this):
        if this.isEmpty():
            return None
        try:
            this.mc.lock()

            topindex = this.mc.get( this.mcQueue_top )
            tailindex = this.mc.get( this.mcQueue_tail )
            if topindex == None or tailindex == None:
                return None
            if( topindex == tailindex ):
                this.mc.unlock()
                return None

            topindex = ( topindex + 1 ) % this.maxVolume

            ret = this.mc.get( this.index_name + str(topindex) )
            this.mc.delete(this.index_name + str(topindex))
            this.mc.set( this.mcQueue_top , topindex )

            this.mc.unlock()
            return ret

        except Exception , e:
            print e
            this.mc.unlock()
            return None


    def popif(this , val):
        if this.isEmpty():
            return False
        try:
            this.mc.lock()

            topindex = this.mc.get( this.mcQueue_top )
            tailindex = this.mc.get( this.mcQueue_tail )
            if topindex == None or tailindex == None:
                return False
            if( topindex == tailindex ):
                this.mc.unlock()
                return False

            topindex = ( topindex + 1 ) % this.maxVolume

            topVal = this.mc.get( this.index_name + str(topindex) )
            if topVal == val:
                this.mc.delete(this.index_name + str(topindex))
                this.mc.set( this.mcQueue_top , topindex )
                ret = True
            else:
                ret = False

            this.mc.unlock()
            return ret

        except Exception , e:
            print e
            this.mc.unlock()
            return False


    def clear(this):
        try:
            while this.pop() != None: pass
            this.mc.lock()
            this.mc.set( this.mcQueue_top , 0 )
            this.mc.set( this.mcQueue_tail , 0 )
            this.mc.unlock()
        except Exception , e:
            print e
            this.mc.unlock()
            return None





