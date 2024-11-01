import sys
import lab5


if __name__ == '__main__':
    assert len(sys.argv) == 2, 'wrong input'
    
    env = lab5.load(sys.argv[1])
    
    path = lab5.generate_path(env)
    lab5.print_path(path)
    
    # env = lab5.draw(env, path)
    env = lab5.draw_lines(env, path)
    
    lab5.show(env)   
    