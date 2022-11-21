// Lista doblemente enlazada
class Node {
    init(value) {
        this.value = value;
        this.next = nil;
        this.prev = nil;
    }
}

class DLL {
    init() {
        this.head = Node(nil);
        this.tail = Node(nil);
        this.head.next = this.tail;
        this.tail.prev = this.head;
        this.length = 0;
    }
    push(value) {
        var new = Node(value);
        new.next = this.head.next;
        new.prev = this.head;
        this.head.next.prev = new;
        this.head.next = new;
        this.length = this.length + 1;
    }
    append(value) {
        var new = Node(value);
        new.next = this.tail;
        new.prev = this.tail.prev;
        this.tail.prev.next = new;
        this.tail.prev = new;
        this.length = this.length + 1;
    }
    setValue(index, value) {
        if (index >= this.length || index < 0) {
            return false;
        }end_if
        var i = 0;
        var currNode = this.head.next;
        while (currNode.next != nil) {
            if (i == index) {
                currNode.value = value;
                return;
            }end_if
            currNode = currNode.next;
        }
    }
    printDLL() {
        var currNode = this.head.next;
        while (currNode.next != nil) {
            print curNode.value;
            currNode = currNode.next;
        }
    }
}

var dll = DLL();
print "DLL: ";
for (var i = 0; i < 10; i = i + 1) {
    dll.push(i);
}
for (var i = 0; i < 10; i = i + 1) {
    dll.append(i);
}
dll.printDLL();
print "DLL Length:";
print dll.length;
dll.setValue(0, 89);
print "DLL: ";
dll.printDLL();
print "DLL Length:";
print dll.length;
